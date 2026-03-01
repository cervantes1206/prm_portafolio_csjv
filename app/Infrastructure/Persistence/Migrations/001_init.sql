CREATE DATABASE IF NOT EXISTS prm_portafolio;
USE prm_portafolio;

CREATE TABLE IF NOT EXISTS estudiantes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  grado VARCHAR(10) NOT NULL,
  frase_personal TEXT,
  fortalezas TEXT,
  retos TEXT,
  talentos TEXT,
  intereses TEXT,
  experiencias TEXT,
  logros TEXT,
  estudios TEXT,
  valores TEXT,
  trayectoria TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
