import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Insect } from './insect';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  private url: string = "http://localhost:8080/insects"

  constructor(private http: HttpClient) {
  }

  getInsectsWhere(searchAttribute: String, value: String) {
    // spajanje url-a s query parametrom
    // za search attribute je moguce i 'wildcard'! Provjeriti na serveru.
    let query: string = this.url + '?' + searchAttribute + '=' + value
    return this.http.get<any>(query);
  }

  getAllInsects() {
    return this.http.get<any>(this.url);
  }

}
