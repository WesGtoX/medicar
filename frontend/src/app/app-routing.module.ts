import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './components/template/login/login.component';
import { RegisterComponent } from './components/template/register/register.component'
import { ConsultationListComponent } from './components/template/consultation-list/consultation-list.component';
import { ConsultationCreateComponent } from './components/template/consultation-create/consultation-create.component'

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: ConsultationListComponent },
  { path: 'list', component: ConsultationCreateComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
