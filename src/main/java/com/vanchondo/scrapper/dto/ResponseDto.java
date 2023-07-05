package com.vanchondo.scrapper.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import lombok.Data;


@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class ResponseDto<T> {
    
    private String message;
    private boolean success;
    private T result;
}
