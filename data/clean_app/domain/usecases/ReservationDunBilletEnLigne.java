package org.enspy.4gi.domain.usecases;

import org.enspy.4gi.domain.usecases.UseCase;
import org.enspy.4gi.domain.dto.ReservationdunbilletenligneDto;
import org.enspy.4gi.domain.responses.ReservationdunbilletenligneResponse;

public class ReservationDunBilletEnLigneUseCase implements UseCase<ReservationDunBilletEnLigneDto,ReservationDunBilletEnLigneResponse> {
    
    @Override
    public ReservationDunBilletEnLigneResponse execute(ReservationDunBilletEnLigneDto dto) {
        //TODO: Implement the use case logic here base on the AI
        System.out.println("ReservationdunbilletenligneUseCase.execute");
        return new ReservationdunbilletenligneResponse();
    }
}