import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  goToIndex() {
    console.log("INDEX")
    this.router.navigate(['/', 'home']);
  }
  goToAbout() {
    console.log("ABOUT")
    this.router.navigate(['/', 'about']);
  }
  goToJson() {
    console.log("JSON")
    this.router.navigate(['/', 'json']);
  }
  goToCsv() {
    console.log("CSV")
    this.router.navigate(['/', 'csv']);
  }
  goToInsects() {
    console.log("insects")
    this.router.navigate(['/', 'insects']);
  }

  getRouter(): Router {
    return this.router;
  }

}
