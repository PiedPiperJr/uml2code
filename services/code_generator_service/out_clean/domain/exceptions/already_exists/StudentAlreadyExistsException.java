package mwm.domain.exceptions.already_exists;

import mwm.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class StudentAlreadyExistsException extends EntityAlreadyExistsException {
public StudentAlreadyExistsException(String message) {
        super(message);
    }
}