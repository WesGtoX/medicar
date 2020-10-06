import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MainService } from 'src/app/main.service';
import { User } from 'src/app/user';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  submitted = false;

  constructor(
    private formBuilder: FormBuilder, 
    private mainService: MainService,
    private router: Router
  ) { }

  ngOnInit() {
    this.registerForm = this.formBuilder.group({
      'first_name': ['', [Validators.required]],
      'email': ['', [Validators.required]],
      'password1': ['', [Validators.required, Validators.minLength(6)]],
      'password2': ['', [Validators.required, Validators.minLength(6)]],
    }, { validator: this.matchingPasswords });
  }

  matchingPasswords(group: FormGroup) {
    if (group) {
      const password1 = group.controls['password1'].value;
      const password2 = group.controls['password2'].value;
      if (password1 === password2) {
        return null;
      }
    }
    return { matching: false };
  }

  onSubmit() {
    let u: User = {
      ...this.registerForm.value, 
      password: this.registerForm.value.password1
    };
    this.mainService.register(u).subscribe(() => {
      let credentials = {
        username: this.registerForm.value.email,
        password: this.registerForm.value.password
      }
      this.mainService.login(credentials).subscribe(() => {
        this.router.navigate(['home']);
      });
    }, (err) => {
      console.error(err);
    });
  }
}
