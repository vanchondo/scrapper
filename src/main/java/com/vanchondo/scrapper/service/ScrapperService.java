package com.vanchondo.scrapper.service;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.itextpdf.text.Document;
import com.itextpdf.text.Image;
import com.itextpdf.text.pdf.PdfWriter;
import com.vanchondo.scrapper.dto.DataDto;
import com.vanchondo.scrapper.dto.ResponseDto;

import io.github.bonigarcia.wdm.WebDriverManager;
import lombok.AllArgsConstructor;
import lombok.extern.log4j.Log4j2;

@Log4j2
@AllArgsConstructor
@Service
public class ScrapperService {
    private final String onePieceId = "dfc7ecb5-e9b3-4aa5-a61b-a498993cd935";
    private final String baseUrl = "http://107.155.106.254/ver/manga/One-Piece/";

    private RestTemplate restTemplate;

    public void startDownload(double start, double end) throws Exception {
        String rootFolder = "OnePieceManga";
        createFolder(rootFolder);
        log.info("Setting up WebDriver...");

        log.info("Get all chapters...");
        List<LinkedHashMap<String, Object>> chapters = getAll(onePieceId);
        log.info("Found {} chapters", chapters.size());

        WebDriverManager.chromedriver().setup();
        WebDriver driver = new ChromeDriver();

        for (LinkedHashMap<String, Object> chapter : chapters) {
            String chapterNumber = chapter.get("FriendlyChapterNumberUrl").toString();
            double currentChapter = convertToDouble(chapterNumber);
            if (currentChapter >= start && currentChapter <= end){
                String identification = chapter.get("Identification").toString();
                int pageCount = (int)chapter.get("PagesCount");
                
                log.info("Chapter={} pages={}", chapterNumber, pageCount);
                String chapterFolder = rootFolder + "/" + getName(chapterNumber, "0000");
                createFolder(chapterFolder);    
                
                openPage(driver, baseUrl + chapterNumber + "/" + identification);
                List<WebElement> pages = driver.findElements(By.className("ImageContainer"));
                String serverImages = "https://pack-yak.intomanga.com/images/manga/One-Piece/chapter/%s/page/%s/%s";
                int currentPageNumber = 1;
                for (WebElement page : pages) {
                    String id = page.getAttribute("id");
                    String imageUrl = String.format(serverImages, chapterNumber, currentPageNumber, id);
                    downloadFile(imageUrl, chapterFolder + "/" + getName(currentPageNumber + "", "00") + ".jpeg");
                    currentPageNumber++;
                }

                mergeAllImagesInFolder(chapterFolder, rootFolder + "/" + getName(chapterNumber, "0000") + ".pdf");
                deleteFolder(chapterFolder);
            }
        }
        driver.quit();
    }

    private void createFolder(String folderName) {
        File rootFolder = new File(folderName);
        if (!rootFolder.exists()) {
            log.info("Creating folder {}", folderName);
            rootFolder.mkdirs();
        }        
    }

    private void deleteFile(String fileName) {
        File rootFolder = new File(fileName);
        if (rootFolder.exists()) {
            log.info("Deleting file {}", fileName);
            rootFolder.delete();
        } 
    }

    private void deleteFolder(String fileName) throws IOException{
        File rootFolder = new File(fileName);
        if (rootFolder.exists()) {
            log.info("Deleting folder {}", fileName);
            FileUtils.deleteDirectory(rootFolder);
        } 
    }

    private String getName(String name, String prefix) {
        return (prefix + name).substring(name.length());
    }

    private void openPage(WebDriver driver, String url) { 
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        driver.manage().window().maximize();
        driver.get(url);
    }

    private List<LinkedHashMap<String, Object>> getAll(String id) throws Exception {
        String urlString = "http://107.155.106.254/chapter/getall?mangaIdentification=" + onePieceId;
        ResponseEntity<DataDto> response = restTemplate.exchange(urlString, HttpMethod.GET, null, new ParameterizedTypeReference<>() {});
        String data = Optional.ofNullable(response.getBody())
            .map(DataDto::getData)
            .orElse(null);
        ResponseDto<List<LinkedHashMap>> responseList = new ObjectMapper().readValue(data, ResponseDto.class);
        List<LinkedHashMap<String, Object>> list = Optional.ofNullable(responseList)
            .map(ResponseDto::getResult)
            .map(List.class::cast)
            .orElse(Collections.emptyList());
        
        sort(list);
        return list;
    }

    private void sort(List<LinkedHashMap<String, Object>> list) {
        list.sort((p1,p2) -> {
            Double chapter1 = convertToDouble(p1.get("FriendlyChapterNumberUrl").toString());
            Double chapter2 = convertToDouble(p2.get("FriendlyChapterNumberUrl").toString());
            
            return chapter1.compareTo(chapter2);
        });
    }

    private Double convertToDouble(String name) {
        return Double.parseDouble(name.replace("-", "."));
    }

    private void downloadFile(String url, String fileName) throws IOException {
        log.info("Downloading url={}", url);
        FileUtils.copyURLToFile(
            new URL(url), 
            new File(fileName)
        );     
    }

    private void mergeAllImagesInFolder(String folder, String pdfName) throws Exception {
        deleteFile(pdfName);
        File chapterFolder = new File(folder);
        List<File> pages = filterImages(chapterFolder.listFiles());
        Document document = new Document();
        PdfWriter writer = PdfWriter.getInstance(document, new FileOutputStream(pdfName));
        document.open();
        for (File page : pages) {
            Image image = Image.getInstance(page.getAbsolutePath());
            float scaler = ((document.getPageSize().getWidth() - document.leftMargin()
               - document.rightMargin()) / image.getWidth()) * 100;

            image.scalePercent(scaler);
            document.add(image);
            document.newPage();
        }
        document.close();    
        writer.close();

    }

    private List<File> filterImages(File[] files) {
        return Stream.of(files).sorted().filter(file -> file.getName().contains(".jpeg")).collect(Collectors.toList());
    }
}
