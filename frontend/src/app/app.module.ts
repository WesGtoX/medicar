import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderComponent } from './components/template/header/header.component';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { LoginComponent } from './components/template/login/login.component';
import { RegisterComponent } from './components/template/register/register.component';
import { ConsultationListComponent } from './components/template/consultation-list/consultation-list.component';
import { ConsultationCreateComponent } from './components/template/consultation-create/consultation-create.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ConsultationListComponent,
    LoginComponent,
    RegisterComponent,
    ConsultationCreateComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
