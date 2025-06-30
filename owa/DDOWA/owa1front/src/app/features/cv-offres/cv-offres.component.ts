import { Component, OnInit } from '@angular/core';
import { CvService, CV } from '../../core/cv.service';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject, of } from 'rxjs';
import { catchError, tap, finalize } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cvs-offre',
  templateUrl: './cv-offres.component.html',
  styleUrls: ['./cv-offres.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class CvsOffreComponent implements OnInit {
  cvs$ = new BehaviorSubject<{ cvs: CV[]; loading: boolean; error: string | null }>({
    cvs: [],
    loading: true,
    error: null,
  });

  offreId: number = 0;

  constructor(private cvService: CvService, private route: ActivatedRoute,private router: Router) {}

  ngOnInit() {
    this.offreId = Number(this.route.snapshot.paramMap.get('id'));
    if (!this.offreId) {
      this.cvs$.next({ cvs: [], loading: false, error: "ID de l'offre manquant" });
      return;
    }
    this.loadCvs();
  }

  loadCvs() {
    this.cvs$.next({ cvs: [], loading: true, error: null });
    this.cvService.getCvsForOffre(this.offreId).pipe(
      catchError(() => {
        this.cvs$.next({ cvs: [], loading: false, error: "Erreur lors du chargement des CVs." });
        return of([]);
      }),
      tap((cvs) => this.cvs$.next({ cvs, loading: false, error: null }))
    ).subscribe();
  }

  getCvUrl(file: string) {
    return file.startsWith('http') ? file : `http://127.0.0.1:8000${file}`;
  }

  classifyAll() {
    const cvs = this.cvs$.value.cvs;
    if (!cvs.length) return;
    this.cvs$.next({ ...this.cvs$.value, loading: true });
    const ids = cvs.map(cv => cv.id);
    console.log(ids)
    this.cvService.classifyBatch(ids).pipe(
      finalize(() => this.cvs$.next({ ...this.cvs$.value, loading: false }))
    ).subscribe({
      next: (results) => {
        // Affichage simple : un résumé par alert
        let txt = results.map((r: any) =>
          `CV ${r.id}: ${r.result.map((pred: any) =>
            `${pred.label} (${Math.round(pred.probability*100)}%)`
          ).join(', ')}`
        ).join('\n\n');
        alert('Résultats de la classification :\n\n' + txt);
      },
      error: () => alert("Erreur lors de la classification en masse")
    });
  }
  goToCvClasses() {
    // Naviguer vers /cv-classes/:offreId (tu adaptes selon ton routing Angular)
    this.router.navigate(['/cv-classes', this.offreId]);
  }


  
}
