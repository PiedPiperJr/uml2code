package org.enspy.4gi.domain.usecases;

import org.enspy.4gi.domain.usecases.UseCase;
import org.enspy.4gi.domain.dto.PublicationdecontenuDto;
import org.enspy.4gi.domain.responses.PublicationdecontenuResponse;

public class PublicationDeContenuUseCase implements UseCase<PublicationDeContenuDto,PublicationDeContenuResponse> {
    
    @Override
    public PublicationDeContenuResponse execute(PublicationDeContenuDto dto) {
        //TODO: Implement the use case logic here base on the AI
        System.out.println("PublicationdecontenuUseCase.execute");
        return new PublicationdecontenuResponse();
    }
}