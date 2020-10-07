import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { TokenInterceptorService } from './token-interceptor.service';
import { AuthGuard } from './auth.guard';

import { LoginComponent } from './components/template/login/login.component';
import { RegisterComponent } from './components/template/register/register.component'
import { ConsultationListComponent } from './components/template/consultation-list/consultation-list.component';
import { ConsultationCreateComponent } from './components/template/consultation-create/consultation-create.component'

const routes: Routes = [
  { path: 'home', component: ConsultationListComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'create', component: ConsultationCreateComponent, canActivate: [AuthGuard] },
  { path: '', redirectTo: '/home', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptorService,
      multi: true
    }
  ],
})
export class AppRoutingModule { }
