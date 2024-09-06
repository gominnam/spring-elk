package com.example.springelk.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class ViewController {

    @GetMapping("/home")
    public String home() {
        return "home";
    }

    @GetMapping("/view/popup")
    public String getMoviePopup() {
        return "movie-detail-popup";
    }
}
