-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: 30-Abr-2022 às 00:01
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
-- Estrutura da tabela `tc_positions`
--

CREATE TABLE `tc_positions` (
  `id` int(11) NOT NULL,
  `protocol` varchar(128) DEFAULT NULL,
  `deviceid` int(11) NOT NULL,
  `servertime` timestamp NOT NULL DEFAULT current_timestamp(),
  `devicetime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `fixtime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `valid` bit(1) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `altitude` float NOT NULL,
  `speed` float NOT NULL,
  `course` float NOT NULL,
  `address` varchar(512) DEFAULT NULL,
  `attributes` varchar(4000) DEFAULT NULL,
  `accuracy` double NOT NULL DEFAULT 0,
  `network` varchar(4000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Extraindo dados da tabela `tc_positions`
--

INSERT INTO `tc_positions` (`id`, `protocol`, `deviceid`, `servertime`, `devicetime`, `fixtime`, `valid`, `latitude`, `longitude`, `altitude`, `speed`, `course`, `address`, `attributes`, `accuracy`, `network`) VALUES
(1, 'watch', 1, '2022-04-30 06:01:11', '2022-04-30 06:00:59', '2022-04-30 06:00:59', b'1', -23.591596, -46.685212, 0, 0, 0, NULL, '{\"sat\":9,\"rssi\":44,\"batteryLevel\":41,\"steps\":0,\"distance\":0.24,\"totalDistance\":1,\"motion\":false,\"hours\":1}', 0, '{\"radioType\":\"gsm\",\"considerIp\":false,\"cellTowers\":[{\"cellId\":1,\"locationAreaCode\":1,\"mobileCountryCode\":7,\"mobileNetworkCode\":2,\"signalStrength\":4},{\"cellId\":1,\"locationAreaCode\":1931,\"mobileCountryCode\":724,\"mobileNetworkCode\":23,\"signalStrength\":44},{\"cellId\":1,\"locationAreaCode\":4,\"mobileCountryCode\":7,\"mobileNetworkCode\":2,\"signalStrength\":4},{\"cellId\":1,\"locationAreaCode\":1,\"mobileCountryCode\":7,\"mobileNetworkCode\":2,\"signalStrength\":4}]}'),
(2, 'watch', 1, '2022-04-30 06:01:19', '2022-04-30 06:01:09', '2022-04-30 06:01:09', b'1', -23.591596, -46.685212, 0, 0, 0, NULL, '{\"sat\":9,\"rssi\":44,\"batteryLevel\":41,\"steps\":0,\"distance\":0.0,\"totalDistance\":1,\"motion\":false,\"hours\":1}', 0, '{\"radioType\":\"gsm\",\"considerIp\":false,\"cellTowers\":[{\"cellId\":1,\"locationAreaCode\":1,\"mobileCountryCode\":7,\"mobileNetworkCode\":2,\"signalStrength\":4},{\"cellId\":1,\"locationAreaCode\":1931,\"mobileCountryCode\":724,\"mobileNetworkCode\":23,\"signalStrength\":44},{\"cellId\":1,\"locationAreaCode\":4,\"mobileCountryCode\":7,\"mobileNetworkCode\":2,\"signalStrength\":4},{\"cellId\":1,\"locationAreaCode\":1,\"mobileCountryCode\":7,\"mobileNetworkCode\":2,\"signalStrength\":4}]}');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tc_positions`
--
ALTER TABLE `tc_positions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_positions_deviceid` (`deviceid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tc_positions`
--
ALTER TABLE `tc_positions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53770;
--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `tc_positions`
--
ALTER TABLE `tc_positions`
  ADD CONSTRAINT `fk_positions_deviceid` FOREIGN KEY (`deviceid`) REFERENCES `tc_devices` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
