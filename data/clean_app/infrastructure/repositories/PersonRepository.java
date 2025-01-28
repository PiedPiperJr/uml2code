package org.enspy.4gi.infrastructure.repositories;

import org.enspy.4gi.domain.entities.Person;
import org.enspy.4gi.domain.repositories.IPersonRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface PersonJpaRepository extends JpaRepository< Person, UUID>, IPersonRepository< Person, UUID>
{
    //TODO: Implement the repository logic here base on the AI
}