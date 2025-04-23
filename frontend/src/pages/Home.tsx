import { useNavigate } from 'react-router-dom';
import { useState, useEffect, ReactNode } from 'react';
import styles from './Home.module.css';
import axios from '../config/axios';  // Importamos nuestra instancia configurada de axios
import { Dialog } from '../components/Dialog';
import { Loader } from '../components/Loader';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import 'dayjs/locale/es';

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
        // Aquí podrías implementar un manejo de errores más elaborado
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const retiroData = {
        corresponsal_id: parseInt(formData.corresponsalId),
        monto: parseInt(formData.monto),
        fecha_hora: formData.fechaHora,
        canal_atencion: formData.canal
      };

      // Creamos dos promesas: una para el tiempo mínimo y otra para la petición
      const minLoadingTime = new Promise(resolve => setTimeout(resolve, 3000));
      const apiCall = axios.post('/retiros', retiroData);

      // Esperamos a que ambas promesas se completen
      await Promise.all([minLoadingTime, apiCall]);

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
      let errorMessage
      if (error.response?.data?.detail) {
        if (error.response?.data?.detail?.message) {
          errorMessage = (
            <>
              <p>{error.response.data.detail.message}</p>
              <p>Intentos: {error.response.data.detail?.intentos}</p>
            </>
          );
        } else {
          errorMessage = error.response.data.detail
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

              <div className={styles.formGroup}>
                <label htmlFor="monto">Monto de Retiro (COP)</label>
                <input
                  type="number"
                  id="monto"
                  name="monto"
                  // min="10000"
                  // max="1000000"
                  value={formData.monto}
                  onChange={handleInputChange}
                  required
                  className={styles.input}
                  placeholder="Entre $10.000 y $1.000.000"
                />
              </div>

              <div className={styles.formGroup}>
                <label htmlFor="fechaHora">Fecha y Hora</label>
                <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="es">
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
                        placeholder: "Seleccione fecha y hora",
                        className: styles.input,
                        fullWidth: true
                      },
                      actionBar: {
                        actions: ['cancel', 'today', 'accept',]
                      }
                    }}
                    timeSteps={{ minutes: 1 }}
                    format="DD/MM/YYYY HH:mm"
                    ampm={false}
                    views={['year', 'month', 'day', 'hours', 'minutes']}
                  />
                </LocalizationProvider>
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

              <button type="submit" className={styles.submitButton}>
                Procesar Retiro
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
                <li className={styles.ruleItem}>
                  Retiros entre $10.000 y $1.000.000 COP
                </li>
                <li className={styles.ruleItem}>
                  Horario de retiros: 7:00 AM - 7:00 PM
                </li>
                <li className={styles.ruleItem}>
                  Límite diario por corresponsal
                </li>
                <li className={styles.ruleItem}>
                  Verificación y autorización requerida
                </li>
                <li className={styles.ruleItem}>
                  Registro detallado de operaciones
                </li>
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
        autoClose={false}
        buttonText={dialogState.type === 'success' ? 'Entendido' : 'Intentar de nuevo'}
      />
      <nav className={styles.navbar}>
        <h1 className={styles.logo}>ADN Técnico</h1>
        <button onClick={handleLogout} className={styles.logoutButton}>
          Cerrar Sesión
        </button>
      </nav>

      <div className={styles.mainContainer}>
        <div className={styles.tabContainer}>
          <div className={styles.tabHeader}>
            <button
              className={`${styles.tab} ${activeTab === 1 ? styles.activeTab : ''}`}
              onClick={() => setActiveTab(1)}
            >
              Sistema
            </button>
            <button
              className={`${styles.tab} ${activeTab === 2 ? styles.activeTab : ''}`}
              onClick={() => setActiveTab(2)}
            >
              Detalles
            </button>
          </div>
          <div className={styles.tabContent}>
            {renderTabContent()}
          </div>
        </div>
      </div>
    </div>
  );
}

