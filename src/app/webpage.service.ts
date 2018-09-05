import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';

import { Website } from 'src/app/website';
import { Observable } from '../../node_modules/rxjs/internal/observable';

@Injectable({
  providedIn: 'root'
})
export class WebsiteFormService {

  constructor(private http: HttpClient) { }
  result;
  takeWebsiteCoord(url, XPATH1, XPATH2: String , timer:number): Observable<Object> {
    return this.http
      .post('/api/add',{"url":url,"productXPATH":XPATH1,"valueXPATH":XPATH2,"timer":timer});
  }
  getDataBase(): Observable<Object>{
    return this.http
      .get('/api/find');
  }
 
}
