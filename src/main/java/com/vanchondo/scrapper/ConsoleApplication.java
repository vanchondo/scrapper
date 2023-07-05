/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package com.vanchondo.scrapper;

import org.springframework.boot.Banner;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

import com.vanchondo.scrapper.service.ScrapperService;

import lombok.AllArgsConstructor;
import lombok.extern.log4j.Log4j2;

@Log4j2
@AllArgsConstructor
@ComponentScan(basePackages = "com.vanchondo")
@SpringBootApplication
public class ConsoleApplication implements CommandLineRunner {

    private static double START = 1;
    private static double END = 1090;

    private ScrapperService scrapperService;

    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(ConsoleApplication.class);
        // disable spring banner
        app.setBannerMode(Banner.Mode.OFF);
        app.run(args);
    }

    @Override
    public void run(String... args) throws Exception {
        log.info("ConsoleApplication::run::Starting app");
        scrapperService.startDownload(START, END);
    }
}