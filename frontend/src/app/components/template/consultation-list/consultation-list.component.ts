import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MainService } from 'src/app/main.service';


@Component({
  selector: 'app-consultation-list',
  templateUrl: './consultation-list.component.html',
  styleUrls: ['./consultation-list.component.css']
})
export class ConsultationListComponent implements OnInit {

  consultations = [];

  constructor(private mainService: MainService, private router: Router) { }

  ngOnInit() {
    this.mainService.getConsultations()
      .subscribe(data => this.consultations = data)
  }

  onUnmark(id: number) {
    this.mainService.deleteConsultation(id).subscribe(() => {
      this.ngOnInit()
    })
  }
}
