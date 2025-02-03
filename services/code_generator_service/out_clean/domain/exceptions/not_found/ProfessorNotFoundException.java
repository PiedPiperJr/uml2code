package mwm.domain.exceptions.not_found;

import mwm.domain.exceptions.EntityNotFoundException;

public class ProfessorNotFoundException extends EntityNotFoundException {
public ProfessorNotFoundException(String message) {
        super(message);
    }
}