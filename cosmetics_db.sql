-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 21, 2025 at 12:06 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cosmetics_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `skin_tone` varchar(255) NOT NULL,
  `texture` varchar(255) NOT NULL,
  `conditiontype` varchar(255) NOT NULL,
  `link` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `category`, `skin_tone`, `texture`, `conditiontype`, `link`) VALUES
(1, 'Foundation A', 'Foundation', 'Fair', 'Smooth', 'Dry', 'http://example.com/foundation-a'),
(2, 'Foundation B', 'Foundation', 'Medium', 'Rough', 'Oily', 'http://example.com/foundation-b'),
(3, 'Lipstick X', 'Lipstick', 'Dark', 'Smooth', 'Oily', 'http://example.com/lipstick-x'),
(4, 'Blush Y', 'Blush', 'Fair', 'Smooth', 'Oily', 'http://example.com/blush-y'),
(5, 'Concealer Z', 'Concealer', 'Medium', 'Rough', 'Dry', 'http://example.com/concealer-z'),
(6, 'Foundation A', 'Foundation', 'Fair', 'Smooth', 'Dry', 'http://example.com/foundation-a'),
(7, 'Foundation B', 'Foundation', 'Medium', 'Rough', 'Oily', 'http://example.com/foundation-b'),
(9, 'Blush Y', 'Blush', 'Fair', 'Smooth', 'Oily', 'http://example.com/blush-y'),
(10, 'Concealer Z', 'Concealer', 'Medium', 'Rough', 'Dry', 'http://example.com/concealer-z');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
