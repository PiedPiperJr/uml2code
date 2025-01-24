package org.enspy.4gi.domain.exceptions.already_exists;

import org.enspy.4gi.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class ProfessorAlreadyExistsException extends EntityAlreadyExistsException {
public ProfessorAlreadyExistsException(String message) {
        super(message);
    }
}