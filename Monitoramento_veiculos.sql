-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: 29-Abr-2022 às 23:59
-- Versão do servidor: 10.3.27-MariaDB-0+deb10u1
-- PHP Version: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `traccar`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `Monitoramento_veiculos`
--

CREATE TABLE `Monitoramento_veiculos` (
  `ID` int(11) NOT NULL,
  `BATERIA_FRACA` tinyint(1) DEFAULT NULL,
  `EM_MOVIMENTO` tinyint(1) DEFAULT NULL,
  `DISTANCIA` text DEFAULT NULL,
  `ULTIMO_MOVIMENTO` text DEFAULT NULL,
  `TIMESTAMP` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Extraindo dados da tabela `Monitoramento_veiculos`
--

INSERT INTO `Monitoramento_veiculos` (`ID`, `BATERIA_FRACA`, `EM_MOVIMENTO`, `DISTANCIA`, `ULTIMO_MOVIMENTO`, `TIMESTAMP`) VALUES
(1, 1, 0, '0.23675216768415988', '2022-04-29 23:23:43.514063', '2022-04-29 23:45:19.223184');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Monitoramento_veiculos`
--
ALTER TABLE `Monitoramento_veiculos`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Monitoramento_veiculos`
--
ALTER TABLE `Monitoramento_veiculos`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
