// metier.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Metier {
  id?: number;
  nom: string;
  description: string;
}

@Injectable({
  providedIn: 'root'
})
export class MetierService {
  private apiUrl = 'http://localhost:8000/api/metiers/';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Metier[]> {
    return this.http.get<Metier[]>(this.apiUrl);
  }

  get(id: number): Observable<Metier> {
    return this.http.get<Metier>(`${this.apiUrl}${id}/`);
  }

  create(metier: Metier): Observable<Metier> {
    return this.http.post<Metier>(this.apiUrl, metier);
  }

  update(id: number, metier: Metier): Observable<Metier> {
    return this.http.put<Metier>(`${this.apiUrl}${id}/`, metier);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}
