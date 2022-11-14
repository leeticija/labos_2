import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-json',
  templateUrl: './json.component.html',
  styleUrls: ['./json.component.css']
})
export class JsonComponent implements OnInit {

  data: any = ""
  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getJson().subscribe(response => {
      this.data = response
      console.log("got data:",this.data)
      console.log("response: ", response)
    })
   }

  // async getData(): Promise<any> {
  //   let j = this.http.get("http://localhost:8080/data").subscribe(
  //     response =>{
  //       //this.data = JSON.parse(Response)
  //       console.log("response in getData(json): ", response)
  //       this.data = response.toString
  //       return response;
  //     })
  //   return j
  // }

  getJson() {
    return this.http.get("http://localhost:8080/data/json");
  }
}
