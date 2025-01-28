package org.enspy.4gi.domain.exceptions.not_found;

import org.enspy.4gi.domain.exceptions.EntityNotFoundException;

public class PersonNotFoundException extends EntityNotFoundException {
public PersonNotFoundException(String message) {
        super(message);
    }
}