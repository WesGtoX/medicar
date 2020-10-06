import { Component, OnInit } from '@angular/core';
import { MainService } from 'src/app/main.service';


@Component({
  selector: 'app-consultation-list',
  templateUrl: './consultation-list.component.html',
  styleUrls: ['./consultation-list.component.css']
})
export class ConsultationListComponent implements OnInit {

  consultations = [];

  constructor(private mainService: MainService) { }

  ngOnInit() {
    this.mainService.getConsultations()
      .subscribe(data => this.consultations = data)
  }
}
