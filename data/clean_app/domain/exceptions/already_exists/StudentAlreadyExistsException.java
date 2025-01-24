package org.enspy.4gi.domain.exceptions.already_exists;

import org.enspy.4gi.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class StudentAlreadyExistsException extends EntityAlreadyExistsException {
public StudentAlreadyExistsException(String message) {
        super(message);
    }
}