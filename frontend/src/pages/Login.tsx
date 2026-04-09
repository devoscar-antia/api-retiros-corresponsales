import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';
import styles from './Login.module.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await authService.login({
        correo: email,
        clave: password,
      });

      localStorage.setItem('token', response.access_token);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error en el login');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <aside className={styles.brand} aria-hidden="true">
        <div className={styles.brandInner}>
          <span className={styles.brandBadge}>Corresponsales</span>
          <h1 className={styles.brandTitle}>Operaciones claras, clientes tranquilos</h1>
          <p className={styles.brandLead}>
            Registre retiros con validaciones de monto, horario y límites diarios en un
            solo lugar.
          </p>
        </div>
      </aside>

      <div className={styles.panel}>
        <div className={styles.loginCard}>
          <header className={styles.header}>
            <p className={styles.eyebrow}>ADN Técnico</p>
            <h2 className={styles.title}>Iniciar sesión</h2>
            <p className={styles.subtitle}>Use su correo corporativo para continuar</p>
          </header>

          <form onSubmit={handleSubmit} className={styles.form} noValidate>
            {error ? (
              <div className={styles.error} role="alert">
                {error}
              </div>
            ) : null}

            <div className={styles.formGroup}>
              <label className={styles.label} htmlFor="login-email">
                Correo electrónico
              </label>
              <input
                id="login-email"
                name="email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={styles.input}
                placeholder="nombre@empresa.com"
                disabled={isLoading}
                required
                aria-invalid={!!error}
              />
            </div>

            <div className={styles.formGroup}>
              <label className={styles.label} htmlFor="login-password">
                Contraseña
              </label>
              <input
                id="login-password"
                name="password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={styles.input}
                placeholder="Su contraseña"
                disabled={isLoading}
                required
                aria-invalid={!!error}
              />
            </div>

            <button type="submit" className={styles.button} disabled={isLoading}>
              {isLoading ? 'Verificando…' : 'Entrar'}
            </button>
          </form>

          <p className={styles.footerNote}>
            Si olvidó su clave, contacte al administrador del sistema.
          </p>
        </div>
      </div>
    </div>
  );
}
