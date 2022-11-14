export class Insect {

  id: Number;
  orderId: Number;
  binomialName: String;
  specie: String;
  genus: String;
  orderName: String;
  orderCommonName: String;
  wings: String;
  totalSpeciesInOrder: Number;
  totalFamilies: Number;
  metamorphosis: String;

  constructor(id?: Number, orderId?: Number, binomialName?: String, specie?: String, genus?: String, 
    orderName?: String, orderCommonName?: String, wings?: String, totalSpeciesInOrder?: Number, totalFamilies?: Number, metamorphosis?: String)
    {
      this.id = id ?? 0;
      this.orderId = orderId??0;
      this.binomialName = binomialName??"";
      this.specie = specie??"";
      this.genus = genus??"";
      this.orderName = orderName??"";
      this.orderCommonName = orderCommonName??"";
      this.wings = wings??"";
      this.totalSpeciesInOrder = totalSpeciesInOrder??0;
      this.totalFamilies = totalFamilies??0;
      this.metamorphosis = metamorphosis??"";
    }
  setId(id: Number) {
    this.id = id;
  }
  setOrderId(id: Number) {
    this.orderId = id;
  }
  setbinomialName(name: String) {
    this.binomialName = name;
  }
  setSpecie(specie: String) {
    this.specie = specie;
  }
  setGenus(genus: String) {
    this.genus = genus;
  }
  setOrderName(order: String) {
    this.orderName = order;
  }
  setOrderCommonName(commonName: String) {
    this.orderCommonName = commonName;
  }
  setWings(wings: String) {
    this.wings = wings;
  }
  setTotalSpeciesInOrder(totalSpecies: Number) {
    this.totalSpeciesInOrder = totalSpecies;
  }
  setTotalFamilies(totalFamilies: Number) {
    this.totalFamilies = totalFamilies;
  }
  setMetamorphosis(metamorphosis: String) {
    this.metamorphosis = metamorphosis;
  }
}
