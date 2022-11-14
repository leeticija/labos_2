import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { AppComponent } from './app.component';
import { CsvComponent } from './csv/csv.component';
import { HomeComponent } from './home/home.component';
import { InsectComponent } from './insect/insect.component';
import { JsonComponent } from './json/json.component';

const routes: Routes = [
  {path : 'home', component : HomeComponent},
  {path : 'about', component : AboutComponent},
  {path : 'csv', component : CsvComponent},
  {path : 'json', component : JsonComponent},
  {path : 'insects', component : InsectComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
