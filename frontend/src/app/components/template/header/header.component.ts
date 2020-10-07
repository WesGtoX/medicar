import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MainService } from 'src/app/main.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  user: string;

  constructor(private mainService: MainService) {
    this.user = localStorage.getItem('name');
  }

  ngOnInit(): void {
  }

  onClick() {
    this.mainService.logout()
  }
}
