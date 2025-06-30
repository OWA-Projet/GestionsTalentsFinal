import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PostulerService {
  private apiUrl = 'http://localhost:8000/api/postuler/';

  constructor(private http: HttpClient) {}

  /**
   * Postule à une offre avec un CV donné.
   * @param offreId ID de l'offre d'emploi
   * @param cvId    ID du CV à utiliser pour postuler
   */
  postuler(offreId: number, cvId: number): Observable<any> {
    return this.http.post<any>(this.apiUrl, {
      offre_id: offreId,
      cv_id: cvId
    });
  }
}
