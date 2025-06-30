import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";


export interface User {
  id: number;
  username: string;
  email?: string;
  nom:string;
  prenom:string;
  // Ajoute d'autres champs si tu veux
}

export interface CV {
  id: number;
  owner: User;
  formations: string;
  experiences: string;
  competences: string;
  langues?: string;
  fichier?: string;
  uploaded_at?: string;
  // Ajoute d'autres champs selon besoin
}
@Injectable({ providedIn: 'root' })
export class CvService {
  private api = 'http://127.0.0.1:8000/api/cvs/';
  private apiCandidat = 'http://localhost:8000/api/cvs_candidat/';

  constructor(private http: HttpClient) {}

  getAll() { return this.http.get<any[]>(this.api); }
  create(fd: FormData) { return this.http.post(this.api, fd); }
  createCVcandidat(fd: FormData) { console.log("HHHHHH");return this.http.post(this.apiCandidat, fd); }
  delete(id: number) { return this.http.delete(`${this.api}${id}/`); }
  classify(id: number) { return this.http.post<any>(`${this.api}${id}/classify/`, {}); }
  getOne(id: number) { return this.http.get<any>(`${this.api}${id}/`); }
  getCvsForOffre(offreId: number): Observable<CV[]> {
    return this.http.get<CV[]>(`${this.api}${offreId}/cvs/`);
  }
  classifyBatch(ids: number[]) {
    return this.http.post<any>('http://127.0.0.1:8000/api/cvs/classify_batch/', { ids });
  }
  getCvsClassificationForOffre(offreId: number) {
    return this.http.get<any[]>(`http://127.0.0.1:8000/api/offres-emploi/${offreId}/cvs-classification/`);
  }

  sendTestEmail(offreId: number, cvOffreIds: number[]) {
    return this.http.post<{success: boolean}>(`http://127.0.0.1:8000/api/offres-emploi/${offreId}/send-tests/`, {
      cv_offre_ids: cvOffreIds
    });
  }
 getOffresSelectionnees() {
  return this.http.get<any[]>('http://127.0.0.1:8000/api/offres-emploi/offres-selectionnees/');
}
getQCMForOffre(offreId: number) {
  return this.http.get<{questions: any[]}>(`http://127.0.0.1:8000/api/offres-emploi/${offreId}/generate-qcm/`);
}
storeScore(offreId: number, cvOffreId: number, score: number) {
  return this.http.post(
    `http://127.0.0.1:8000/api/offres-emploi/${offreId}/store-score/`,
    { score: score, cv_offre_id: cvOffreId }
  );
}

  
  
}
