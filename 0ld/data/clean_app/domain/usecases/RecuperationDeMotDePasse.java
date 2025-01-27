package org.enspy.4gi.domain.usecases;

import org.enspy.4gi.domain.usecases.UseCase;
import org.enspy.4gi.domain.dto.RecuperationdemotdepasseDto;
import org.enspy.4gi.domain.responses.RecuperationdemotdepasseResponse;

public class RecuperationDeMotDePasseUseCase implements UseCase<RecuperationDeMotDePasseDto,RecuperationDeMotDePasseResponse> {
    
    @Override
    public RecuperationDeMotDePasseResponse execute(RecuperationDeMotDePasseDto dto) {
        //TODO: Implement the use case logic here base on the AI
        System.out.println("RecuperationdemotdepasseUseCase.execute");
        return new RecuperationdemotdepasseResponse();
    }
}