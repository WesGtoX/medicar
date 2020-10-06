import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { User } from './user';
import { Specialty } from './specialty';
import { Doctor } from './doctor';
import { Agenda } from './agenda';
import { Consultation } from './consultation'


@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private http: HttpClient) { }

  url = 'http://192.168.15.21:8000'

  // authentications
  register(data: User): Observable<User> {
    return this.http.post<User>(`${this.url}/users/`, data);
  }

  login(credentials: { username: string, password: string }): Observable<any> {
    try {
      return this.http.post(`${this.url}/api-token-auth/`, credentials);
    } catch (error) {
      console.log(error)
    }
  }

  // specialties
  getSpecialties(): Observable<Specialty[]> {
    return this.http.get<Specialty[]>(`${this.url}/medicos/`);
  }

  // doctors
  getDoctorsFilterSpecialties(specialtyId: number): Observable<Doctor[]> {
    return this.http.get<Doctor[]>(`${this.url}/medicos/?specialty=${specialtyId}`);
  }

  // agendas
  getAgendasFilterDoctors(doctorId: number): Observable<Agenda[]> {
    return this.http.get<Agenda[]>(`${this.url}/agendas/?doctor=${doctorId}`);
  }

  // consultations
  postConsultations(data: Consultation): Observable<Consultation[]> {
    return this.http.post<Consultation[]>(`${this.url}/consultas/`, data);
  }

  getConsultations(): Observable<Consultation[]> {
    return this.http.get<Consultation[]>(`${this.url}/consultas/`);
  }

  deleteConsultations(id: number) {
    return this.http.get(`${this.url}/consultas/${id}`);
  }  
}
