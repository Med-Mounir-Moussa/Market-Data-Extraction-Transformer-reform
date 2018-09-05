import { Component, OnInit } from '@angular/core';
import { Website } from '../website' ;
import { FormGroup,FormBuilder,Validators } from '../../../node_modules/@angular/forms';
import { WebsiteFormService } from '../../../src/app/webpage.service';
import { HttpClientModule } from '@angular/common/http'; 

@Component({
  selector: 'app-website-form',
  templateUrl: './website-form.component.html',
  styleUrls: ['./website-form.component.css']
})

export class WebsiteFormComponent implements OnInit {

  result : string;
  constructor (private webService:WebsiteFormService) {} ;
  model = new Website("https://bloomberg.com/markets/currencies",
                    "/html/body/div[5]/main/div/div/div[3]/div[4]/div/table/tbody/tr[1]/td[1]/a/div[2]",
                    "/html/body/div[5]/main/div/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]"
                  ,null);
  submitted = false;
  timedSubmit = false;
  msg(){
    console.log("msg")
    this.timedSubmit = true;
  }
  onSubmit() {
   
    this.submitted = true ;
      console.log(this.model.timer);
      console.log(this.submitted);
    
    console.log(this.model.url);
    console.log(this.model.productXPATH);
    console.log(this.model.valueXPATH);
    this.webService.takeWebsiteCoord(this.model.url,this.model.productXPATH,this.model.valueXPATH,this.model.timer).subscribe((data : string) => this.result = data);
    console.log(this.result)
    this.webService.getDataBase();
  }

  ngOnInit() {
  }



}
