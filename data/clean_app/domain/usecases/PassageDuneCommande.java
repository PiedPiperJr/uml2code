package org.enspy.4gi.domain.usecases;

import org.enspy.4gi.domain.usecases.UseCase;
import org.enspy.4gi.domain.dto.PassagedunecommandeDto;
import org.enspy.4gi.domain.responses.PassagedunecommandeResponse;

public class PassageDuneCommandeUseCase implements UseCase<PassageDuneCommandeDto,PassageDuneCommandeResponse> {
    
    @Override
    public PassageDuneCommandeResponse execute(PassageDuneCommandeDto dto) {
        //TODO: Implement the use case logic here base on the AI
        System.out.println("PassagedunecommandeUseCase.execute");
        return new PassagedunecommandeResponse();
    }
}