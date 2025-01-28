package org.enspy.4gi.domain.usecases;

import org.enspy.4gi.domain.usecases.UseCase;
import org.enspy.4gi.domain.dto.AuthentificationutilisateurDto;
import org.enspy.4gi.domain.responses.AuthentificationutilisateurResponse;

public class AuthentificationUtilisateurUseCase implements UseCase<AuthentificationUtilisateurDto,AuthentificationUtilisateurResponse> {
    
    @Override
    public AuthentificationUtilisateurResponse execute(AuthentificationUtilisateurDto dto) {
        //TODO: Implement the use case logic here base on the AI
        System.out.println("AuthentificationutilisateurUseCase.execute");
        return new AuthentificationutilisateurResponse();
    }
}