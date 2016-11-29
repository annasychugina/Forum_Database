
--
-- Table structure for table `Follow`
--

DROP TABLE IF EXISTS `Follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Follow` (
  `follower` varchar(50) DEFAULT NULL,
  `following` varchar(50) DEFAULT NULL,
  CONSTRAINT `Follow_ibfk_1` FOREIGN KEY (`follower`) REFERENCES `User` (`email`),
  CONSTRAINT `Follow_ibfk_2` FOREIGN KEY (`following`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Follow`
--

LOCK TABLES `Follow` WRITE;
/*!40000 ALTER TABLE `Follow` DISABLE KEYS */;
/*!40000 ALTER TABLE `Follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Forum`
--

DROP TABLE IF EXISTS `Forum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Forum` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(126) CHARACTER SET utf8 DEFAULT NULL,
  `short_name` varchar(50) NOT NULL,
  `user` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `Forum_ibfk_1` FOREIGN KEY (`user`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Forum`
--

LOCK TABLES `Forum` WRITE;
/*!40000 ALTER TABLE `Forum` DISABLE KEYS */;
/*!40000 ALTER TABLE `Forum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Posts`
--

DROP TABLE IF EXISTS `Posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Posts` (
  `date` datetime DEFAULT NULL,
  `dislikes` int(10) NOT NULL DEFAULT '0',
  `forum` varchar(1024) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `isApproved` tinyint(1) NOT NULL DEFAULT '1',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0',
  `isEdited` tinyint(1) NOT NULL DEFAULT '1',
  `isHighlighted` tinyint(1) NOT NULL DEFAULT '1',
  `isSpam` tinyint(1) NOT NULL DEFAULT '0',
  `likes` int(10) NOT NULL DEFAULT '0',
  `message` varchar(1024) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `thread` int(10) DEFAULT NULL,
  `parent` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Posts`
--

LOCK TABLES `Posts` WRITE;
/*!40000 ALTER TABLE `Posts` DISABLE KEYS */;
/*!40000 ALTER TABLE `Posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Subscribe`
--

DROP TABLE IF EXISTS `Subscribe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Subscribe` (
  `subscriber` varchar(50) NOT NULL,
  `subscription` int(10) NOT NULL,
  CONSTRAINT `Subscribe_ibfk_1` FOREIGN KEY (`subscriber`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Subscribe`
--

LOCK TABLES `Subscribe` WRITE;
/*!40000 ALTER TABLE `Subscribe` DISABLE KEYS */;
/*!40000 ALTER TABLE `Subscribe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Thread`
--

DROP TABLE IF EXISTS `Thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Thread` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `isClosed` tinyint(1) DEFAULT NULL,
  `isDeleted` tinyint(1) DEFAULT NULL,
  `title` text CHARACTER SET utf8,
  `slug` varchar(250) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `message` varchar(5000) DEFAULT NULL,
  `forum` varchar(50) NOT NULL,
  `user` varchar(50) DEFAULT NULL,
  `likes` int(10) NOT NULL DEFAULT '0',
  `dislikes` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  CONSTRAINT `Thread_ibfk_1` FOREIGN KEY (`user`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Thread`
--

LOCK TABLES `Thread` WRITE;
/*!40000 ALTER TABLE `Thread` DISABLE KEYS */;
/*!40000 ALTER TABLE `Thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `about` text CHARACTER SET utf8,
  `email` varchar(50) NOT NULL,
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `isAnonymous` tinyint(1) DEFAULT NULL,
  `name` varchar(30) CHARACTER SET utf8 DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`email`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
--  for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-20 20:30:21
