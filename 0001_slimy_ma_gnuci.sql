CREATE TABLE `scanResults` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`filename` varchar(255) NOT NULL,
	`timestamp` timestamp NOT NULL DEFAULT (now()),
	`predictionResult` varchar(50) NOT NULL,
	`confidenceScore` int NOT NULL,
	`peFeatures` text,
	CONSTRAINT `scanResults_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
ALTER TABLE `scanResults` ADD CONSTRAINT `scanResults_userId_users_id_fk` FOREIGN KEY (`userId`) REFERENCES `users`(`id`) ON DELETE no action ON UPDATE no action;
