import { Component, OnInit } from '@angular/core';
import { CvService } from '../../core/cv.service';
import { CommonModule } from '@angular/common';
import { BehaviorSubject, of } from 'rxjs';
import { catchError, finalize, tap } from 'rxjs/operators';
import { Router } from '@angular/router';

@Component({
  selector: 'app-espace-candidat',
  templateUrl: './espace-candidat.component.html',
  styleUrls: ['./espace-candidat.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class EspaceCandidatComponent implements OnInit {
  offresSelectionnees$ = new BehaviorSubject<any[]>([]);
  loading$ = new BehaviorSubject<boolean>(true);
  error$ = new BehaviorSubject<string | null>(null);

  constructor(private cvService: CvService, private router: Router) {}

  ngOnInit() {
    this.loading$.next(true);
    this.error$.next(null);
    this.cvService.getOffresSelectionnees().pipe(
      tap((offres) => this.offresSelectionnees$.next(offres)),
      catchError(() => {
        this.error$.next('Erreur lors du chargement.');
        this.offresSelectionnees$.next([]);
        return of([]);
      }),
      finalize(() => this.loading$.next(false))
    ).subscribe();
  }

  passerTest(offreId: number, cvOffreId: number) {
    this.router.navigate(['/qcm', offreId, { cvOffreId }]); // Passage de l'id de la liaison
  }
}
