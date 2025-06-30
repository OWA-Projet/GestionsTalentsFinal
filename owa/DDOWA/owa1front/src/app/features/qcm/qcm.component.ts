import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CvService } from '../../core/cv.service';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Observable, of } from 'rxjs';
import { switchMap, map, catchError, startWith } from 'rxjs/operators';

@Component({
  selector: 'app-qcm',
  templateUrl: './qcm.component.html',
  styleUrls: ['./qcm.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class QcmComponent {
  questions$: Observable<any[]>;
  loading$: Observable<boolean>;
  error$: Observable<string | null>;

  userAnswers: { [key: number]: string } = {};
  submitted = false;
  score = 0;
  scoreSent = false;
  sendError: string | null = null;

  cvOffreId: number | null = null;
  offreId: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private cvService: CvService
  ) {
    this.offreId = Number(this.route.snapshot.paramMap.get('offreId'));
    this.cvOffreId = Number(this.route.snapshot.paramMap.get('cvOffreId'));

    const qcm$ = of(this.offreId).pipe(
      switchMap(offreId => {
        if (!offreId) return of({ questions: [], error: 'ID offre invalide' });
        return this.cvService.getQCMForOffre(offreId).pipe(
          map(res => ({ questions: res.questions || [], error: null })),
          catchError(() => of({ questions: [], error: 'Erreur de chargement' })),
          startWith({ questions: [], error: null }) // état loading
        );
      })
    );

    this.questions$ = qcm$.pipe(map(x => x.questions));
    this.error$ = qcm$.pipe(map(x => x.error));
    this.loading$ = qcm$.pipe(map(x => x.questions.length === 0 && !x.error));
  }

  selectAnswer(qId: number, choice: string) {
    this.userAnswers[qId] = choice;
  }

  submit(questions: any[]) {
    this.submitted = true;
    this.scoreSent = false;
    this.sendError = null;

    let correct = 0;
    questions.forEach(q => {
      if (this.userAnswers[q.id] === q.answer) correct++;
    });
    this.score = correct;

    // Envoi du score au backend AVEC l’id cv_offre !
    if (this.offreId && this.cvOffreId) {
      this.cvService.storeScore(this.offreId, this.cvOffreId, this.score)
        .subscribe({
          next: () => { this.scoreSent = true; },
          error: err => { this.sendError = "Erreur lors de l'enregistrement du score."; }
        });
    }
  }

  get answeredCount(): number {
    return Object.keys(this.userAnswers).length;
  }
}
