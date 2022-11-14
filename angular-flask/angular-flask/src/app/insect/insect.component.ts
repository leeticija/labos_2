import { Component, EventEmitter, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Insect } from '../insect';
import { RestService } from '../rest.service';

@Component({
  selector: 'app-insect',
  templateUrl: './insect.component.html',
  styleUrls: ['./insect.component.css']
})
export class InsectComponent implements OnInit {

  dataSource = [{"order_id": 1, "order_name": "Mantodea"}, {"order_id":3, "order_name":"Sept"}]
  displayedColumns = ["order_id", "order_name"]
  dataArray = [{"name":"insect1", "features":"feat1"}, {"name":"insect2", "features":"feat2"}]
  rows: String[] = []
  data: any = {}
  csv: String = ""
  searchInput = "";
  // ne mijenjati poredak ovoga u listi!:
  attributes: any[] = ["insect_id","order_id", "binomial_name", "specie", "genus", "order_name", "order_common_name","wings", "total_order_species", "total_order_families", "metamorphosis"]
  searchableAttributes: String[] = ["binomial_name", "specie", "genus", "order_name", "order_common_name","wings", "total_order_species", "total_order_families", "metamorphosis"]
  selectedItem: any = "wildcard"
  // ------------------------
  insects: Insect[] = []

  constructor(private http: HttpClient, public rs: RestService) {}

  ngOnInit() {
    this.rs.getAllInsects().subscribe((response) => {
      //console.log("response on all insects: ", response)
      this.data = <JSON>response
      this.insects = this.serializeJsonsToInsectsList(this.data["data"])
    })
   }
   serializeJsonsToInsectsList (jsonList: any): Insect[] {
    let insects: Insect[] = []
    for(let jsn of jsonList) {
      console.log("ONE JSON: ", jsn)
      let genus = jsn[this.attributes[4]]
      let insect: Insect = new Insect()
      insect.setId(jsn[this.attributes[0]])
      insect.setOrderId(jsn[this.attributes[1]])
      insect.setbinomialName(jsn[this.attributes[2]])
      insect.setSpecie(jsn[this.attributes[3]])
      insect.setGenus(genus)
      insect.setOrderName(jsn[this.attributes[5]])
      insect.setOrderCommonName(jsn[this.attributes[6]])
      insect.setWings(jsn[this.attributes[7]])
      insect.setTotalSpeciesInOrder(jsn[this.attributes[8]])
      insect.setTotalFamilies(jsn[this.attributes[9]])
      insect.setMetamorphosis(jsn[this.attributes[10]])
      insects.push(insect)
      console.log("insect: ", insect)
      console.log("genus: ", genus)
    }
    return insects
   }

  getJson() {
    return this.http.get("http://localhost:8080/data/json");
  }

  changeSelectedItem(value: string) {
    console.log(value)
    this.selectedItem = value
  }

  searchCallback() {
    // request server for insects that contain only attributes with selected value
    console.log("sending search request!")
    // this.insects = [this.insect1] // tu samo promijenim listu insekata i sve se samo updatea
    console.log("SEARCHING FOR: ", this.selectedItem, " ", this.searchInput)
    this.rs.getInsectsWhere(this.selectedItem, this.searchInput).subscribe((response) => {
      this.data = <JSON>response
      this.insects = this.serializeJsonsToInsectsList(this.data["data"])
    })
  }
  parseCsv(csv: String) {
    let rows: String[]
    rows = this.csv.split(/\r?\n/);
    // content tablice, bez pocetnog headera s nazivima stupca
    let content = []
    console.log("RETCI KOD PARSIRANJA: ", rows)
    for(let i = 0; i < rows.length; i++) {
      console.log("one row: ", rows[i])
    }

  }

}

