import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { MainService } from './main.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  
  constructor(
    public authService: MainService,
    private router : Router
  ) {}

  canActivate()  {
    if (!this.checkToken()) {
      this.router.navigate(["login"]);
    } else {
      return true;
    } 
  }

  public checkToken() {
    return !!localStorage.getItem("token");
  }
}