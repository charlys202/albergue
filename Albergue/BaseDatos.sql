-- 1. Crear base de datos
CREATE DATABASE AlbergueFrontera;
GO
USE AlbergueFrontera;
GO

-- 2. Tablas principales

-- Personas albergadas
CREATE TABLE PersonasAlbergadas (
    id_persona INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    genero VARCHAR(20),
    edad INT,
    nacionalidad VARCHAR(50),
    fecha_ingreso DATE NOT NULL,
    fecha_egreso DATE NULL,
    estado_salud VARCHAR(100),
    observaciones TEXT
);

-- Voluntarios / personal
CREATE TABLE Voluntarios (
    id_voluntario INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(100),
    rol VARCHAR(50),
    horario_trabajo VARCHAR(100),
    activo BIT DEFAULT 1
);

-- Recursos (inventario)
CREATE TABLE Recursos (
    id_recurso INT IDENTITY(1,1) PRIMARY KEY,
    nombre_recurso VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50),
    cantidad_disponible INT NOT NULL,
    unidad VARCHAR(20),
    fecha_ultima_actualizacion DATETIME DEFAULT GETDATE()
);

-- Donaciones recibidas
CREATE TABLE Donaciones (
    id_donacion INT IDENTITY(1,1) PRIMARY KEY,
    nombre_donante VARCHAR(100),
    id_recurso INT,
    cantidad INT NOT NULL,
    unidad VARCHAR(20),
    fecha_donacion DATE NOT NULL DEFAULT GETDATE(),
    observaciones TEXT,
    FOREIGN KEY (id_recurso) REFERENCES Recursos(id_recurso)
);

-- Camas asignables
CREATE TABLE Camas (
    id_cama INT IDENTITY(1,1) PRIMARY KEY,
    numero_cama INT NOT NULL,
    habitacion VARCHAR(50),
    estado VARCHAR(20) NOT NULL DEFAULT 'disponible',
    id_persona INT NULL,
    FOREIGN KEY (id_persona) REFERENCES PersonasAlbergadas(id_persona)
);

-- Usuarios del sistema
CREATE TABLE UsuariosSistema (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contraseña_hash VARCHAR(200) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    nombre_completo VARCHAR(150),
    correo VARCHAR(100),
    activo BIT DEFAULT 1
);

-- Historial de movimientos de personas
CREATE TABLE HistorialMovimientos (
    id_movimiento INT IDENTITY(1,1) PRIMARY KEY,
    id_persona INT NOT NULL,
    tipo_movimiento VARCHAR(50) NOT NULL, -- ingreso, traslado, egreso
    fecha DATETIME NOT NULL DEFAULT GETDATE(),
    observaciones TEXT,
    FOREIGN KEY (id_persona) REFERENCES PersonasAlbergadas(id_persona)
);
-- Graficas --
CREATE TABLE Suministros (
    id_suministro INT PRIMARY KEY IDENTITY(1,1),
    tipo_suministro NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(255),
    cantidad INT NOT NULL DEFAULT 0,
    unidad_medida NVARCHAR(50), -- kg, litros, piezas, etc.
    fecha_ingreso DATE DEFAULT GETDATE(),
    fecha_vencimiento DATE,
    proveedor NVARCHAR(150),
    estado NVARCHAR(50) DEFAULT 'Disponible', -- Disponible, Agotado, Por vencer
    observaciones NVARCHAR(500)
);

-- Insertar datos de ejemplo
INSERT INTO Suministros (tipo_suministro, descripcion, cantidad, unidad_medida, proveedor, estado) VALUES
('Alimentos', 'Arroz, frijoles, aceite', 450, 'kg', 'Donación Municipal', 'Disponible'),
('Medicinas', 'Medicamentos básicos', 250, 'piezas', 'Cruz Roja', 'Disponible'),
('Ropa', 'Ropa de abrigo y básica', 200, 'piezas', 'Donaciones Particulares', 'Disponible'),
('Otros', 'Artículos de higiene y limpieza', 100, 'piezas', 'ONG Local', 'Disponible');

-- Tabla para registrar salidas de personas (opcional)
CREATE TABLE SalidasPersonas (
    id_salida INT PRIMARY KEY IDENTITY(1,1),
    id_persona INT FOREIGN KEY REFERENCES PersonasAlbergadas(id_persona),
    fecha_salida DATE NOT NULL DEFAULT GETDATE(),
    motivo_salida NVARCHAR(200), -- Traslado, Reunificación familiar, etc.
    destino NVARCHAR(200),
    observaciones NVARCHAR(500)
);
