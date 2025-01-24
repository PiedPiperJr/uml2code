package org.enspy.4gi.domain.exceptions.not_found;

import org.enspy.4gi.domain.exceptions.EntityNotFoundException;

public class StudentNotFoundException extends EntityNotFoundException {
public StudentNotFoundException(String message) {
        super(message);
    }
}