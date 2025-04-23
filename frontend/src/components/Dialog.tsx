import { useEffect, useState, ReactNode } from 'react';
import styles from './Dialog.module.css';

interface DialogProps {
  message: string | ReactNode;
  type: 'success' | 'error' | 'info' | 'warning';
  show: boolean;
  onClose: () => void;
  autoClose?: boolean;
  autoCloseTime?: number;
  buttonText?: string;
}

export const Dialog = ({
  message,
  type,
  show,
  onClose,
  autoClose = false,
  autoCloseTime = 3000,
  buttonText
}: DialogProps) => {
  const [isHiding, setIsHiding] = useState(false);

  useEffect(() => {
    if (show && autoClose) {
      const timer = setTimeout(() => {
        setIsHiding(true);
        setTimeout(() => {
          setIsHiding(false);
          onClose();
        }, 200);
      }, autoCloseTime);

      return () => clearTimeout(timer);
    }
  }, [show, autoClose, autoCloseTime, onClose]);

  const handleClose = () => {
    setIsHiding(true);
    setTimeout(() => {
      setIsHiding(false);
      onClose();
    }, 200);
  };

  if (!show) return null;

  return (
    <div className={styles.overlay}>
      <div className={`${styles.dialog} ${styles[type]} ${isHiding ? styles.hiding : ''}`}>
        {message && <div className={styles.content}>
          {message}
        </div>}
        {!autoClose && (
          <button
            onClick={handleClose}
            className={`${styles.button} ${styles[`button-${type}`]}`}
          >
            {buttonText || (type === 'success' ? 'OK' : 'Cerrar')}
          </button>
        )}
      </div>
    </div>
  );
}; 