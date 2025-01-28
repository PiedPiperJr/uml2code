package org.enspy.4gi.domain.exceptions.not_found;

import org.enspy.4gi.domain.exceptions.EntityNotFoundException;

public class ProfessorNotFoundException extends EntityNotFoundException {
public ProfessorNotFoundException(String message) {
        super(message);
    }
}