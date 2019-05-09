
CREATE DATABASE dahuadb_face;
use dahuadb_face ;

CREATE TABLE `face_detection_camera`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `camera_name` varchar(100),
    `camera_type` varchar(100),
    `camera_ip` varchar(100),
    `venue_id` varchar(50),
     `device_id` varchar(100),
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
     ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `face_demographics` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
     `api_id` int(11) NOT NULL,
    `timestamp` varchar(100),
    `camera_id` int(11),

    `gender` varchar(50),
    `age` varchar(50),
	`emotion` varchar(50),
    `age_range`  varchar(50),
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`, `api_id`)
     ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

/*!40101 SET character_set_client = @saved_cs_client */;


CREATE TABLE `face_demographics_record`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `timestamp` varchar(100),
    `camera_id` int(11),
    `gender` varchar(50),
    `age` varchar(50),
    `age_range`  varchar(50),
    `beginAge` varchar(100),
    `endAge` varchar(100),
    `emotion` varchar(200),

    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
     ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

/*!40101 SET character_set_client = @saved_cs_client */;
