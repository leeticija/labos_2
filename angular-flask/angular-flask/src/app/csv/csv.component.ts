import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-csv',
  templateUrl: './csv.component.html',
  styleUrls: ['./csv.component.css']
})
export class CsvComponent implements OnInit {

  data: any = {}
  csv: String = ""
  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.getJson().subscribe(response => {
      this.data = <JSON>response
      this.csv = this.data["csv"]
      console.log("got data:",this.data)
      console.log("response: ", response)
    })
   }

  getJson() {
    return this.http.get("http://localhost:8080/data/csv");
  }

}
