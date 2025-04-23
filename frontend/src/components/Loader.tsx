import { useEffect, useState } from 'react';
import styles from './Loader.module.css';

export const Loader = () => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((oldProgress) => {
        const newProgress = oldProgress + 1;
        return newProgress >= 100 ? 100 : newProgress;
      });
    }, 30); // Ajusta la velocidad de la animación

    return () => {
      clearInterval(timer);
    };
  }, []);

  return (
    <div className={styles.loaderOverlay}>
      <div className={styles.loaderContainer}>
        <div className={styles.progressWrapper}>
          <div 
            className={styles.progressBar} 
            style={{ width: `${progress}%` }}
          />
          <span className={styles.progressText}>{progress}%</span>
        </div>
        <p className={styles.loaderText}>Procesando solicitud...</p>
      </div>
    </div>
  );
}; 