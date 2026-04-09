import { useNavigate } from 'react-router-dom';
import { useState, useEffect, ReactNode } from 'react';
import styles from './Home.module.css';
import axios from '../config/axios';
import { Dialog } from '../components/Dialog';
import { Loader } from '../components/Loader';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { esES } from '@mui/x-date-pickers/locales';
import dayjs from 'dayjs';
import 'dayjs/locale/es';
import {
  parseMontoCOP,
  formatMontoCOP,
  sanitizeMontoInput,
} from '../utils/montoCOP';

const localeTextPicker = {
  ...(esES.components.MuiLocalizationProvider.defaultProps?.localeText ?? {}),
  okButtonLabel: 'Aceptar',
};

interface Corresponsal {
  id: number;
  nombre: string;
  tope_diario: string;
}

interface DialogState {
  message: string | ReactNode;
  type: 'success' | 'error' | 'info' | 'warning';
  show: boolean;
}

export default function Home() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(1);
  const [corresponsales, setCorresponsales] = useState<Corresponsal[]>([]);
  const [formData, setFormData] = useState({
    corresponsalId: '',
    monto: '',
    fechaHora: '',
    canal: ''
  });
  const [dialogState, setDialogState] = useState<DialogState>({
    message: '',
    type: 'success',
    show: false
  });
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchCorresponsales = async () => {
      try {
        const { data } = await axios.get('/corresponsales');
        setCorresponsales(data);
      } catch (error) {
        console.error('Error al cargar corresponsales:', error);
      }
    };

    fetchCorresponsales();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement> | Date | dayjs.Dayjs) => {
    if (e instanceof Date || dayjs.isDayjs(e)) {
      const date = dayjs.isDayjs(e) ? e.toDate() : e;
      setFormData(prev => ({
        ...prev,
        fechaHora: date.toISOString().slice(0, 16)
      }));
    } else {
      const { name: inputName, value } = e.target;
      setFormData(prev => ({
        ...prev,
        [inputName]: value
      }));
    }
  };

  const handleMontoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      monto: sanitizeMontoInput(e.target.value),
    }));
  };

  const handleMontoBlur = () => {
    setFormData((prev) => {
      const t = prev.monto.trim();
      if (t === '') {
        return prev;
      }
      const n = parseMontoCOP(prev.monto);
      if (!Number.isFinite(n)) {
        return prev;
      }
      return { ...prev, monto: formatMontoCOP(n) };
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    const montoNum = parseMontoCOP(formData.monto);
    if (!Number.isFinite(montoNum)) {
      setIsLoading(false);
      setDialogState({
        message:
          'Ingrese un monto válido. Use punto para miles y coma para decimales (ej. 50.000 o 25.500,50).',
        type: 'error',
        show: true,
      });
      return;
    }
    if (montoNum < 10_000 || montoNum > 1_000_000) {
      setIsLoading(false);
      setDialogState({
        message: 'El monto debe estar entre $10.000 y $1.000.000 COP.',
        type: 'error',
        show: true,
      });
      return;
    }

    try {
      await axios.post('/retiros', {
        corresponsal_id: parseInt(formData.corresponsalId, 10),
        monto: montoNum,
        fecha_hora: formData.fechaHora,
        canal_atencion: formData.canal,
      });

      setDialogState({
        message: 'Retiro procesado exitosamente',
        type: 'success',
        show: true
      });

      setFormData({
        corresponsalId: '',
        monto: '',
        fechaHora: '',
        canal: ''
      });

    } catch (error: any) {
      let errorMessage;
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'object') {

          if (error.response.data.detail instanceof Array) {
            const errorDetail = error.response.data.detail[0];

            errorMessage = errorDetail ? (
              <p>{errorDetail.msg}</p>
            ) : (
              <p>Error desconocido</p>
            );
          } else {
            errorMessage = (
              <>
                <p>{error.response.data.detail.message}</p>
                {error.response.data.detail.intentos !== undefined && (
                  <p>Intentos: {error.response.data.detail.intentos}</p>
                )}
              </>
            );
          }


        } else {
          errorMessage = error.response.data.detail;
        }
      } else {
        errorMessage = 'Error desconocido';
      }

      setDialogState({
        message: errorMessage,
        type: 'error',
        show: true
      });
      console.error('Error al procesar el retiro:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 1:
        return (
          <div className={styles.formContainer}>
            <h2 className={styles.formTitle}>Solicitud de Retiro</h2>
            <form onSubmit={handleSubmit} className={styles.form}>
              <div className={styles.formGroup}>
                <label htmlFor="corresponsalId">Corresponsal</label>
                <select
                  id="corresponsalId"
                  name="corresponsalId"
                  value={formData.corresponsalId}
                  onChange={handleInputChange}
                  required
                  className={styles.select}
                >
                  <option value="">Seleccione un corresponsal</option>
                  {corresponsales.map(corresponsal => (
                    <option key={corresponsal.id} value={corresponsal.id}>
                      {corresponsal.nombre} - Tope: ${Number(corresponsal.tope_diario).toLocaleString('es-CO')}
                    </option>
                  ))}
                </select>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label htmlFor="monto">Monto (COP)</label>
                  <input
                    type="text"
                    id="monto"
                    name="monto"
                    autoComplete="off"
                    inputMode="decimal"
                    value={formData.monto}
                    onChange={handleMontoChange}
                    onBlur={handleMontoBlur}
                    required
                    className={styles.input}
                    placeholder="Ej. 50.000 o 25.500,50"
                  />
                  <span className={styles.helperText}>
                    Miles con punto (.). Decimales con coma (ej. 1.000,50).
                  </span>
                </div>

                <div className={styles.formGroup}>
                  <label htmlFor="fechaHora">Fecha y hora</label>
                  <LocalizationProvider
                    dateAdapter={AdapterDayjs}
                    adapterLocale="es"
                    localeText={localeTextPicker}
                  >
                    <DateTimePicker
                      value={formData.fechaHora ? dayjs(formData.fechaHora) : null}
                      onChange={(newValue) => {
                        if (newValue) {
                          setFormData(prev => ({
                            ...prev,
                            fechaHora: newValue.format('YYYY-MM-DDTHH:mm')
                          }));
                        }
                      }}
                      slotProps={{
                        textField: {
                          required: true,
                          id: 'fechaHora',
                          placeholder: 'Seleccionar…',
                          className: styles.input,
                          fullWidth: true,
                        },
                        actionBar: {
                          actions: ['cancel', 'today', 'accept'],
                        },
                      }}
                      timeSteps={{ minutes: 1 }}
                      format="DD/MM/YYYY HH:mm"
                      ampm={false}
                      views={['year', 'month', 'day', 'hours', 'minutes']}
                    />
                  </LocalizationProvider>
                </div>
              </div>

              <div className={styles.formGroup}>
                <label htmlFor="canal">Canal de Atención</label>
                <select
                  id="canal"
                  name="canal"
                  value={formData.canal}
                  onChange={handleInputChange}
                  required
                  className={styles.select}
                >
                  <option value="">Seleccione un canal</option>
                  <option value="dispositivo">Dispositivo Móvil</option>
                  <option value="ventanilla">Ventanilla</option>
                  <option value="cajero">Cajero Corresponsal</option>
                  <option value="kiosko">Kiosko Digital</option>
                </select>
              </div>

              <button
                type="submit"
                className={styles.submitButton}
                disabled={isLoading}
              >
                {isLoading ? 'Procesando…' : 'Procesar retiro'}
              </button>
            </form>
          </div>
        );
      case 2:
        return (
          <div>
            <section className={styles.welcomeSection}>
              <h2 className={styles.welcomeTitle}>Panel de Control</h2>
              <p className={styles.welcomeText}>
                Bienvenido al sistema de corresponsales bancarios. Gestiona tus operaciones y transacciones bancarias de manera eficiente y segura.
              </p>
              <p className={styles.welcomeText} style={{ marginTop: '0.75rem' }}>
                Utiliza el panel para acceder a todas las funcionalidades y mantener un registro actualizado de operaciones.
              </p>
            </section>

            <section className={styles.rulesSection}>
              <h3 className={styles.rulesTitle}>Reglas del Sistema</h3>
              <ul className={styles.rulesList}>
                <li className={styles.ruleItem}>Retiros entre $10.000 y $1.000.000 COP</li>
                <li className={styles.ruleItem}>Horario de retiros: 7:00 AM - 7:00 PM</li>
                <li className={styles.ruleItem}>Límite diario por corresponsal</li>
                <li className={styles.ruleItem}>Verificación y autorización requerida</li>
                <li className={styles.ruleItem}>Registro detallado de operaciones</li>
              </ul>
            </section>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      {isLoading && <Loader />}
      <Dialog
        message={dialogState.message}
        type={dialogState.type}
        show={dialogState.show}
        onClose={() => setDialogState(prev => ({ ...prev, show: false }))}
        autoClose={dialogState.type === 'success'}
        buttonText={dialogState.type === 'success' ? 'Entendido' : 'Intentar de nuevo'}
      />
      <header className={styles.navbar}>
        <h1 className={styles.logo}>ADN Técnico</h1>
        <button
          type="button"
          onClick={handleLogout}
          className={styles.logoutButton}
          aria-label="Cerrar sesión"
        >
          <span className={styles.logoutLabelFull}>Cerrar sesión</span>
          <span className={styles.logoutLabelShort} aria-hidden="true">
            Salir
          </span>
        </button>
      </header>

      <main className={styles.mainContainer}>
        <div className={styles.tabContainer}>
          <div
            className={styles.tabHeader}
            role="tablist"
            aria-label="Secciones del panel"
          >
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 1}
              id="tab-sistema"
              aria-controls="tabpanel-sistema"
              className={`${styles.tab} ${activeTab === 1 ? styles.activeTab : ''}`}
              onClick={() => setActiveTab(1)}
            >
              Registrar retiro
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 2}
              id="tab-detalles"
              aria-controls="tabpanel-detalles"
              className={`${styles.tab} ${activeTab === 2 ? styles.activeTab : ''}`}
              onClick={() => setActiveTab(2)}
            >
              Información
            </button>
          </div>
          <div
            className={styles.tabContent}
            role="tabpanel"
            id={activeTab === 1 ? 'tabpanel-sistema' : 'tabpanel-detalles'}
            aria-labelledby={activeTab === 1 ? 'tab-sistema' : 'tab-detalles'}
          >
            {renderTabContent()}
          </div>
        </div>
      </main>
    </div>
  );
}
