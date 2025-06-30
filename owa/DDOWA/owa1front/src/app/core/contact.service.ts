import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ContactForm {
  nom: string;
  email: string;
  sujet: string;
  message: string;
}

@Injectable({ providedIn: 'root' })
export class ContactService {
  private apiUrl = 'http://localhost:8000/api/contact/';

  constructor(private http: HttpClient) {}

  envoyerContact(form: ContactForm): Observable<any> {
    return this.http.post<any>(this.apiUrl, form);
  }
}
