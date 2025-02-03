package mwm.domain.exceptions.already_exists;

import mwm.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class ProfessorAlreadyExistsException extends EntityAlreadyExistsException {
public ProfessorAlreadyExistsException(String message) {
        super(message);
    }
}