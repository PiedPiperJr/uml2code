package org.enspy.4gi.domain.exceptions.already_exists;

import org.enspy.4gi.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class PersonAlreadyExistsException extends EntityAlreadyExistsException {
public PersonAlreadyExistsException(String message) {
        super(message);
    }
}